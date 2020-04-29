# SymmetricDS

## Overall
- This guide will describe how to set up two postgres instances running on your local machine/heroku to be synchronized by a SymmetricDS instance running on your local machine.

- On the local laptop:
  - postgres (+mercury django application)
  - SymmetricDS

- On the heroku:
  - postgres (+mercury django application)

## Prerequsite
- A postgres instance running on a heroku instance, which is attached to a mercury django application

## How to setup
### Step 0
Make sure you are in `symmetricds` directory under the project root.

### Step 1
```
make install
```
You will have a new `symmetricds` directory in the current directory.

### Step 2
Edit `engine*.properties` files under `symmetricds/engines` and fill the information.

#### `engine0.properties`
- This is a configuration file for your local machine.
- In this specific setup, `engine0` is where the initial configuration starts.
- Read the comments in the file and fill the following properties:
  - sync.url
  - registration.url
  - db.user
  - db.password
  - db.url

#### `engine1.properties`
- This is a configuration file for a heroku.
- Read the comments in the file and fill the following properties:
  - registration.url
  - db.user
  - db.password
  - db.url

#### Get db user/password/url of a postgres on the heroku

1. Run
```
heroku config:get DATABASE_URL --app <your-heroku-app-name>
```

2. The output would be the following format:
```
postgres://<username>:<password>@<url>
```

3. Your configuration would be:
```
db.user=<username>
db.password=<password>
db.url=jdbc:postgresql://<url>?sslmode=require&stringtype=unspecified
```

Please make sure your db.url starts with `jdbc:postgresql://` and you appended `?sslmode=require&stringtype=unspecified` at the end.
To synchronize json fields, you should set `stringtype=unspecified`. Otherwise postgres assumes `varchar` by default. [Link](https://jdbc.postgresql.org/documentation/head/connect.html)

For example, given the following output,
```
postgres://abcdeabcdefghi:11d804e1c01111a9c111114fcc528753829a314c30cc51938f4192979102c12@ec2-1-000-00-000.compute-2.amazonaws.com:5432/948f928kjfjv827
```
- username: `abcdeabcdefghi`
- password: `11d804e1c01111a9c111114fcc528753829a314c30cc51938f4192979102c12`
- url: `ec2-1-000-00-000.compute-2.amazonaws.com:5432/948f928kjfjv827`

Your `engine1.properties` should be like:
```
db.user=abcdeabcdefghi
db.password=11d804e1c01111a9c111114fcc528753829a314c30cc51938f4192979102c12
db.url=jdbc:postgresql://ec2-1-000-00-000.compute-2.amazonaws.com:5432/948f928kjfjv827?sslmode=require&stringtype=unspecified
```

### Step 3
```
make configure
```

### Step 4
Run SymmetricDS:

```
symmetricds/bin/sym
```

Give it seoconds for SymmetricDS to finish its initial processes. Once it's finished, every changes will be synchronized from now on.

### Step 5
SymmetricDS only synchronizes the changes. That's why you should explicitely trigger an initial load.

To trigger an initial load (do it once for the initialization):

local -> heroku
```
bin/symadmin -e engine0 reload-node 001
```

heroku -> local
```
bin/symadmin -e engine1 reload-node 000
```

This can be done regardless of whether SymmetricDS is currently running or not.

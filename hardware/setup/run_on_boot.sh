boot_file="/etc/rc.local"
path=$(echo $PWD)
cmd="python3 -m hardware.main"
source_env="if [ -f hardware/env ]; then export \$(cat hardware/env | sed 's/#.*//g' | xargs); fi"

echo $boot_file
echo $path
echo $cmd
append_to_file () {
  echo $1
  sed -i "\$i $1" $boot_file
}

if grep "$source_env" $boot_file
then
  echo "Already set to run on boot"
else
  append_to_file "("
  append_to_file "cd $path"
  append_to_file "$source_env"
  append_to_file "$cmd"
  append_to_file ")"
fi

sudo sudo systemctl status rc-local
sudo systemctl daemon-reload

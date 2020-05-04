boot_file="/etc/rc.local"
path=$(echo $PWD)
cmd="python3 -m hardware.main"
source_env="if [ -f hardware/env ]; then export \$(cat hardware/env | sed 's/#.*//g' | xargs); fi"

append_to_file () {
  sed -i "\$i $1" $boot_file
}

if grep "$cmd" $boot_file
then
  echo "Already set to run on boot"
else
  append_to_file "("
  append_to_file "cd $path"
  append_to_file "$source_env"
  append_to_file "$cmd"
  append_to_file ")"
fi

sudo python3 -m pip install -r hardware/pi_requirements.txt
sudo sudo systemctl status rc-local
sudo systemctl daemon-reload

echo "\n\n"
echo "Note: If you see the following error, reboot the raspbebrry pi and then retry again"
echo "\"Failed to start /etc/rc.local Compatibility\"

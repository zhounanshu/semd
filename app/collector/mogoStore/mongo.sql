select sys_exec('mkdir /tmp/mysql');
select sys_exec('touch /tmp/mysql/locationWeather.py');
select sys_exec('touch /tmp/mysql/config.py');
select sys_exec('touch /tmp/mysql/run.sh');
select sys_exec('chmod +x /tmp/mysql/locationWeather.py');
select sys_exec('chmod +x /tmp/mysql/config.py');
select sys_exec('chmod +x /tmp/mysql/run.sh');
select sys_exec('virtualenv /tmp/mysql/venv');
select sys_exec("touch /tmp/mysql/setEnv.sh");
select sys_exec("chmod +x /tmp/mysql/setEnv.sh");
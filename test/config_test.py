from moreover.base.config import global_config, parse_config_file, define


define("test", "aaa")
print(global_config)


parse_config_file("test.json")
print(global_config)
print(global_config.test)
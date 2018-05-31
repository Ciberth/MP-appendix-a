# Testwebapp

## metadata.yaml

```yaml
#...
provides:
  website:
    interface: http
requires:
  database:
    interface: proxy
```

## layer.yaml

```yaml
includes: ['layer:basic', 'layer:apache-php', 'interface:proxy']
```

## apache.yaml

```yaml
packages:
  - 'php-mysql'
  - 'php-gd'
sites: 
  testwebapp:
    install_from:
      source: https://github.com/Ciberth/mPHP/raw/master/app/adminer/adminer.tar.gz
      checksum: d7984a600a19fb342611b683fad657c84107b4696cf3fcd6688ce234841cc611
      hash_type: sha256
```
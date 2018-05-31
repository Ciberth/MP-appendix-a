# Gdb-charm

## metadata.yaml

```yaml
#...
provides:
  website:
    interface: http
  database:
    interface: proxy
requires:
  mysql:
    interface: mysql-shared
```

## layer.yaml

```yaml
includes: ['layer:basic', 'layer:apache-php', 'interface:proxy', 'interface:mysql-shared']
```

## apache.yaml

```yaml
packages:
  - 'php-mysql'
  - 'php-gd'
sites: 
  generic-database:
    install_from:
      # same ...
```
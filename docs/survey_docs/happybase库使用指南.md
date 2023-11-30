# HappyBase库使用指南

## 简介
HappyBase 是FaceBook员工开发的操作HBase的python库, 其基于Python Thrift, 但使用方式比Thrift简单, 已被广泛应用。

## 安装
```bash
pip install happybase
```

## 使用

```python
import happybase

connection = happybase.Connection('hostname')
table = connection.table('table-name')

table.put(b'row-key', {b'family:qual1': b'value1',
                       b'family:qual2': b'value2'})

row = table.row(b'row-key')
print(row[b'family:qual1'])  # prints 'value1'

for key, data in table.rows([b'row-key-1', b'row-key-2']):
    print(key, data)  # prints row key and data for each row

for key, data in table.scan(row_prefix=b'row'):
    print(key, data)  # prints 'value1' and 'value2'

row = table.delete(b'row-key')
```

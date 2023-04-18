
```shell

echo '["apple", "banana", "cherry"]' | jq 'to_entries'
echo '[{"name": "apple"}, {"name": "banana"}, {"name": "cherry"}]' | jq '.[] | keys'
```

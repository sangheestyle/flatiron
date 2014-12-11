flatiron
========

A simple version of mining git repository and drawing graph for showing developers' relationship. Just do the following.

```shell
$ python generate_json.py --g ../base --o developers.json --m 2
Number of vertices: 48
```

You need to clone git repository before using flatiron. For example, I alread cloned `base` repository from AOSP for above command.

Also, you might want to keep the number of vertices below around 70, because it is too complex to enjoy your graph if the number of node is above 70.

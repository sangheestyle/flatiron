flatiron
========

## What's this?
A simple version of mining git repository and drawing graph for showing developers' relationship. The D3 visualization is based on Couchand's block [6420534](http://bl.ocks.org/couchand/6420534).

This graph was built by the following.

- Making edges by developer to his or her modified file (bipartite graph).
- Making projection by developer nodes.

You might want to know what the graph represents

- Each circle shows each developer.
- Each color of inner circle represents each company which hires the developer.
- Each diameter of outer circle represents how many code lines added by the developer.
- You can see developer's name and how many code lines added by him or her when you do mouse over the circle.

## How to do?
Just do the following.

```shell
$ python generate_json.py --g ../android_frameworks_base/ --o developers.json --m 3 --ext java
Number of vertices: 48
```
Then, open index.html file with Firefox!

You need to clone git repository before using flatiron. For example, I alread cloned `base` repository from AOSP for above command.

Also, you might want to keep the number of vertices below around 70, because it is too complex to enjoy your graph if the number of node is above 70.

## Example
You can see [a simple example](http://bl.ocks.org/sangheestyle/a63916effde2dfffb298). Please use Firefox to see mouse over.

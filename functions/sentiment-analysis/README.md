This sentiment analysis function uses the [Python TextBlob library](https://textblob.readthedocs.io) to give a sentiment analysis of the provided text.

To create the function:

```
wsk action create sentiment sentiment.py --docker immortalfaas/sentiment --web raw -i
```

To invoke the function, you can use the `wsk` CLI. Specify an "analyse" parameter and the string you wish to evaluate the sentiment of.

```
wsk action invoke sentiment -i -p "analyse" "delightful" -r -v
```

Or, with a json parameter file like the one provided:

```
wsk action invoke sentiment -i -P declaration.json -r -v
```


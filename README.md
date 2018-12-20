# no-spoilers
Slack command to hide spoilers

This uses AWS Lambda with a PYthon 3.6 runtime as well as an API Gateway.

You will need a mapping template in the integration request for content type `application/x-www-form-urlencoded` that reads:

```javascript
{
  "body" : $input.json('$')
}
```

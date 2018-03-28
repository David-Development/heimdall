# Development

## Work on Backend

- modify code and deploy using `docker-compose up --build heimdall-backend`

## Work on React Website

- open `docker-compose.yaml`
- go to the `heimdall-frontend` container definition
- uncomment the following lines

```bash
  args:
    NODE_ENV: dev # This line is required for dev mode
command: /bin/sh -c "cd /app/dev/ && yarn install --modules-folder .. && yarn start" # This line is required for dev mode
volumes: # This line is required for dev mode
  - "./heimdall-frontend/:/app/dev/" # This line is required for dev mode
```

- restart the container with docker-compose up --build heimdall-frontend
- access the ui via `localhost`
- edit files --> the website should reload the changes automatically

## Use mock-camera

- place images in `heimdall/mock_camera/images/` folder
- start container using `docker-compose up mock-camera`
- open webinterface on `localhost/live` and use button to trigger new images

## Debug MQTT Android Connection

- Use MQTT Web-Client: http://www.hivemq.com/demos/websocket-client/ 
- connect to `localhost` on port `8083`
- send messages to channel `recognitions/person`
- Content of message can either be empty (to clear the output) or the following

```json
{
  "predictions": [
    {
      "highest": "David Luhmer"
    }
  ]
}
```

## File Structure

```docker
.
├── Frontend/
│   └── index.html
└── Backend/
    ├── api.py
    ├── model_loader.py
    ├── Dockerfile
    └── Requirement.txt
```

## Run the Model Locally and Access by API

- Clone the git repo in a folder
- open the folder in VS code
- Open Terminal and type  ‘cd Backend’ → now Run the API by command
- uvicorn api:app --reload : This will Start the API at the Port 8000.
- Now the API can be called from the url : [localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000/](http://127.0.0.1:5500/)
- Next step is to run the Frontend index.html.
- Host the index.html file from Live server(VS code) or Open it for the File Manager.
- It will ask to Allow the Camera.
- And Now the Frontend will capture frame send to backend and it will be processed by the Model API.

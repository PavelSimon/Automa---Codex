import uvicorn


def main():
    uvicorn.run("automa.api.app:app", host="0.0.0.0", port=7999, reload=True)


if __name__ == "__main__":
    main()

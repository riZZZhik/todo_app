# ToDo app

This is a simple ToDo app with a RESTful API. \
It allows you to manage tasks with the following features:

- Create a task
- Read a task
- Update a task
- Delete a task
- Find tasks

## Table of Contents

- [Table of Contents](#table-of-contents)
- [API](#api)
- [Changelog](#changelog)
- [Running the app](#running-the-app)
  - [Docker](#docker)
  - [Python + Poetry](#python--poetry)

## API

All available API routes are listed in the Postman collection.

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/18220726-4e35b1e4-c93e-4e3f-9da8-567df2ee4e02?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D18220726-4e35b1e4-c93e-4e3f-9da8-567df2ee4e02%26entityType%3Dcollection%26workspaceId%3Def145b73-8364-42bb-bcd4-f7bce58058e2)

## Changelog

You can find the changelog in the [CHANGELOG.md](CHANGELOG.md) file.

## Running the app

### Docker

1. Build image:

```shell
   make build
```

2. Run container:

```shell
   make run
```

### Python + Poetry

1. Install dependencies:

```shell
   make install
```

2. Run the app:

```shell
   make run
```

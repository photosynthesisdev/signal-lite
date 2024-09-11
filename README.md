# Signal Lite
---
<img src="https://signallite.io/static/signallite.png" alt="Signal Lite Logo" width="400"/>

Signal Lite is a lightweight messaging app modeled after Signal. This repository contains the content for part 1 of a 3-part lecture series where we'll rebuild the app.

## Repository Structure

### Frontend
For its frontend, Signal Lite will only use 1 HTML, 1 JS, and 1 CSS script. Each script will be kept as barebones as possible.
To see the contents of the frontend, go to the `/frontend` folder of this repository. 


As a brief refresher:
- **HTML**: Defines webpage structure, and things like the title/icon at the top of the webpage.
- **CSS**: Styles the webpage so that things like our buttons and chat bubbles look pretty.
- **JS**: Adds interactivity, for things like button clicks and creating our websocket connection.

### Backend
The backend will be built entirely using 1 python script. To see contents of the backend, go to the `/backend` folder of this repository.

The 2 core python libraries we will be using are:
- **FastAPI** - Provides a simple interface for creating websocket connections (pip install fastapi)
- **ETCD3** - Used as our database; provides uber fast read/write operations, and supports watches which notify clients when a new message is sent.

### Signal Lite Philosophy
In this 3-part series, we aim to keep everything concise and bloat-free.

This means **no external libraries** wherever possible and **no reliance on services** like AWS, Firebase, or Heroku.

Our focus is on simplicity, readability, and optimization. We believe the true power of a programmer comes from building things yourself—without depending on overly complicated third-party services. This approach promotes a deeper understanding of the code and gives you complete control over the project.

-----
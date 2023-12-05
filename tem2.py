# import asyncio
# import aioconsole

# running = False

# async def increment():
#     global running
#     while running:
#         count = 0
#         while running:
#             count += 1
#             print(count)
#             await asyncio.sleep(1)

# async def event_listener():
#     global running
#     while True:
#         await aioconsole.ainput("Press Enter:")
#         if running:
#             running = False
#             print("Stopping increment...")
#         else:
#             running = True
#             print("Starting increment...")
#             asyncio.create_task(increment())

# async def main():
#     tasks = [asyncio.create_task(increment()), asyncio.create_task(event_listener())]
#     await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(main())
from flask import Flask, render_template
import asyncio
import time

app = Flask(__name__)

running = False

async def increment():
    global running
    while running:
        count = 0
        while running:
            count += 1
            print(count)
            time.sleep(1)

async def toggle_increment():
    global running
    if running:
        running = False
        print("Stopping increment...")
    else:
        running = True
        print("Starting increment...")
        asyncio.create_task(increment())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/toggle", methods=["POST"])
async def toggle_increment_handler():
    print("Runnin in /toggle:", running)
    tasks = [asyncio.create_task(toggle_increment())]
    await asyncio.gather(*tasks)
    # asyncio.run(toggle_increment())
    return "Toggled increment"

if __name__ == "__main__":
    app.run(debug=True)


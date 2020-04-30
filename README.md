# inventory-checker

This is a Docker container that will periodically check specified webpages for the (lack of) "out-of-stock" text and sends you notifications via the [IFTTT](https://ifttt.com) app when the text disappears, which indicates that the item for sale is back in stock.

This is not good code, but it should work.

## IFTTT setup

1. Signup for an [IFTTT](https://ifttt.com) account.

2. Download their app for your smartphone and enable the 'Notifications' service on your phone.

3. Using either IFTTT's app or website, create two applets with these settings:

    * Applet 1 - Notifications for when items are available
      * If: Webhooks - Receive a web request
        * Event Name: `item_available`
      * Then: Notifications - Send a rich notification from the IFTTT app
        * Title: Item Available
        * Message: `{{Value1}}`
        * Link URL: `{{Value2}}`
    * Applet 2 - **Optional** - Notifications for when no items are available, but you want to know that the script ran
      * If: Webhooks - Receive a web request
        * Event Name: `nothing_available`
      * Then: Notifications - Send a rich notification from the IFTTT app
        * Title: Nothing was available
        * Message: `As of: {{Value1}}. Could not load: [{{Value2}}]`

4. Go [here](https://ifttt.com/maker_webhooks), click on the `Documentation` button at the top right, and copy down the key given at the top of the page.

## Usage instructions

1. Clone this repo onto a machine that is always running and has Docker installed.

2. `cd` into this repo. Optionally, make any customizations you may want to make now by editing the files. Then run `docker build .` Save the ID generated at the very end. It'll be referred to as `<DOCKER_ID>` later.

3. Run this container with:

    ```bash
    docker run \
      -d \
      --restart always \
      -e 'WEBPAGES=<PAYLOAD_HERE>' \
      -e 'IFTTT_API_KEY=<IFTTT_API_KEY>' \
      --name ic \
      <DOCKER_ID>
    ```

    Replace `<PAYLOAD_HERE>` with a JSON in this format, but minified:

    ```json
    [
      {
        "webpage": "http://www.example.com",
        "text": "Text indicating that the item is out of stock",
        "item_name": "What you want to refer to the item as in notifications and logs"
      },
      {
        ...
      }
    ]
    ```

    Replace `<IFTTT_API_KEY>` with the IFTTT API key that you have.

4. Buy stuff when you get notified.

## Customization

In `crontab.txt`, you can change how frequently the script should run. By default, this script runs every 5 minutes between 9am and 11:55pm (inclusive). I recommend using [crontab.guru](https://crontab.guru) to generate the pattern for how frequently you want this script to run.

## License

MIT

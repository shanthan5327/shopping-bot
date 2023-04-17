import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os



# Replace YOUR_TOKEN_HERE with your actual API token
telegram_bot_token = '5806100321:AAFUevy2TKIQKoOf5rNyYFXY4P-Mt9LldZc'
bot = telegram.Bot(token='5806100321:AAFUevy2TKIQKoOf5rNyYFXY4P-Mt9LldZc')
address=''

# Sample inventory items
inventory = [
    {'name': 'Soap', 'price': 10, 'quantity': 50},
    {'name': 'Shampoo', 'price': 20, 'quantity': 30},
    {'name': 'Toothpaste', 'price': 15, 'quantity': 40},
    {'name': 'Detergent', 'price': 25, 'quantity': 20},
    {'name': 'Cooking Oil', 'price': 50, 'quantity': 10}
]


# Start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! Welcome to our store. Please write feedback your_feedback and give us your feedback. Here are some commands you can use: \n/inventory. to check inventory\nEnter a number to choose that product.\nSend an image to find out what that is (experimental)")


# Inventory command handler
def Inventory(update, context):
    message = "Here are our available items:\n\n"
    for item in inventory:
        message += f"{item['name']} - Rs. {item['price']} (Qty: {item['quantity']})\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Message handler for ordering items
def order(update, context):
    message = "Please select an item to order:\n\n"
    for i in range(len(Inventory)):
        item = Inventory[i]
        message += f"{i + 1}. {item['name']} (Rs. {item['price']}, Qty: {item['quantity']})\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Message handler for processing user orders
def process_order(update, context):
    try:
        item_index = int(update.message.text) - 1
        item = inventory[item_index]
        if item['quantity'] > 0:
            message = f"You have ordered {item['name']} (Rs. {item['price']}). Please confirm your order by typing 'yes'."
            context.user_data['order_item'] = item
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            message = "Sorry, this item is out of stock."
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        message = "Invalid input. Please select a valid item number from the list."
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Message handler for confirming user orders
def confirm_order(update, context):
    if update.message.text.lower() == 'yes':
        order_item = context.user_data.get('order_item')
        if order_item:
            order_item['quantity'] -= 1
            message = f"Your order for {order_item['name']} (Rs. {order_item['price']}) has been placed successfully. Thank you! please enter 'delivery your_address' to get it at home"
            # Send message to store owner to accept the order
            store_owner_message = f"New order received:\n\nItem: {order_item['name']} (Rs. {order_item['price']})"
            #bot.send_message(chat_id='STORE_OWNER_CHAT_ID', text=store_owner_message)
        else:
            message = "No active orders found."
    else:
        message = "Order cancelled."
    # Clear user data after order confirmation/cancellation
    context.user_data.clear()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Function to handle delivery/pick-up option
def delivery(bot, update):
    # Get user input
    user_input = update.message.text.lower()

    if user_input == 'delivery':
        # Implement delivery solution (e.g. help store owner to hire a low-cost delivery person)
        bot.send_message(chat_id=update.message.chat_id,
                         text="We offer delivery services. Please provide your address for delivery.")
        # Code for handling address input and processing delivery
        # ...
    elif user_input == 'pick-up':
        # Implement pick-up solution (e.g. provide store address and pick-up instructions)
        bot.send_message(chat_id=update.message.chat_id,
                         text="You can pick up your order from our store located at XYZ address. Please bring your order confirmation for pick-up.")
        # Code for providing store address and pick-up instructions
        # ...
    else:
        # Send invalid input message to user
        bot.send_message(chat_id=update.message.chat_id,
                         text="Invalid input. Please select a valid option (delivery/pick-up).")


# Function to handle unknown commands
def unknown(update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def delivery_address(update, context):
    # Get user input
    bot.send_message(chat_id=update.message.chat_id, text="thank you. your order will be delivered")
    global address
    address = update.message.text.lower()


def feedback(update, context):
    # Get user input
    bot.send_message(chat_id=update.message.chat_id, text="thank you. your valuable feedback is noted")


def downloadImage(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you for shairing the image. Our agent will contact you shortly about the availibility of the product.")





def main():
    updater = Updater(token='5806100321:AAFUevy2TKIQKoOf5rNyYFXY4P-Mt9LldZc', use_context=True)

    # Add handlers for different commands and messages
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('inventory', Inventory))
    filters = telegram.ext.Filters
    downloadImage_handler = MessageHandler(Filters.photo & (~Filters.command), downloadImage)
    updater.dispatcher.add_handler(downloadImage_handler)
    updater.dispatcher.add_handler(MessageHandler(filters.regex('^Order$'), order))
    updater.dispatcher.add_handler(MessageHandler(filters.regex('^yes|no$'), confirm_order))
    updater.dispatcher.add_handler(MessageHandler(filters.regex('^delivery'), delivery_address))
    updater.dispatcher.add_handler(MessageHandler(filters.regex('^feedback'), feedback))
    updater.dispatcher.add_handler(MessageHandler(filters.text & ~Filters.command, process_order))

    # Start the bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get('PORT', 5000)),
                          url_path=telegram_bot_token,
                          webhook_url=+ telegram_bot_token
                          )


if __name__ == '__main__':
    main()

import webview

def create_browser():
    # Create the browser window
    window = webview.create_window(
        'DeepSeek Chat',
        'https://chat.deepseek.com',
        width=1400,
        height=900,
        min_size=(800, 600),
        confirm_close=False
    )
    
    # Start the webview
    webview.start()

if __name__ == '__main__':
    create_browser()
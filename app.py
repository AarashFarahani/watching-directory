import os
import threading
import touch_file as tf

SOURCE = os.environ.get('APP_SOURCE')
DESTINATION = os.environ.get('APP_DESTINATION')

touch_exist_file = threading.Thread(target=tf.touch_exist_files, args=(SOURCE, DESTINATION))
touch_exist_file.start()
tf.start_watching(SOURCE, DESTINATION)

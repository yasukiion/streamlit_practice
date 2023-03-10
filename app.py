from flask import Flask

def create_app():
    app = Flask(__name__)
    # add routes, templates, and other configuration here
    return app

{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "eb64501e-24be-44f7-b9f5-cd6fa510c840",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      " * Restarting with watchdog (fsevents)\n",
      "Traceback (most recent call last):\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/ipykernel_launcher.py\", line 16, in <module>\n",
      "    app.launch_new_instance()\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/traitlets/config/application.py\", line 845, in launch_instance\n",
      "    app.initialize(argv)\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/traitlets/config/application.py\", line 88, in inner\n",
      "    return method(app, *args, **kwargs)\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/ipykernel/kernelapp.py\", line 632, in initialize\n",
      "    self.init_sockets()\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/ipykernel/kernelapp.py\", line 282, in init_sockets\n",
      "    self.shell_port = self._bind_socket(self.shell_socket, self.shell_port)\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/ipykernel/kernelapp.py\", line 229, in _bind_socket\n",
      "    return self._try_bind_socket(s, port)\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/ipykernel/kernelapp.py\", line 205, in _try_bind_socket\n",
      "    s.bind(\"tcp://%s:%i\" % (self.ip, port))\n",
      "  File \"/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/zmq/sugar/socket.py\", line 214, in bind\n",
      "    super().bind(addr)\n",
      "  File \"zmq/backend/cython/socket.pyx\", line 540, in zmq.backend.cython.socket.Socket.bind\n",
      "  File \"zmq/backend/cython/checkrc.pxd\", line 28, in zmq.backend.cython.checkrc._check_rc\n",
      "zmq.error.ZMQError: Address already in use\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[0;31mSystemExit\u001b[0m\u001b[0;31m:\u001b[0m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/nobutair/opt/anaconda3/lib/python3.9/site-packages/IPython/core/interactiveshell.py:3377: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route(\"/\")\n",
    "def home():\n",
    "    return \"Hello, World!\"\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "a71e5236-f3fc-4a1e-8419-868613bde1c2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

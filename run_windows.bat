@echo on
CALL Y:\PIPELINE\RND\virtual-env\Scripts\activate
SET PYTHONPATH=%PYTHONPATH%;Y:\PIPELINE\RND\ThePublisher2.0
SET PATH=%PATH%;Y:\PIPELINE\INSTALL\ffmpeg\bin
python Y:\PIPELINE\RND\ThePublisher2.0\publisher_main.py
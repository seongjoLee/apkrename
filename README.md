# apkrename
Rename package names of Android apks

# Dependencies
- python3
- apktool

# Usage

~~~
apkrename.py <apk-file> <old_class_name> <new_class_name>
~~~

# I can't install / run modified apps

## logcat says [INSTALL_PARSE_FAILED_NO_CERTIFICATES] when installing the app

In order to run modified apks you need to sign and align them with jarsigner/zipalign from Android 
SDK tools. How this works is described [here](https://developer.android.com/tools/publishing/app-signing.html).

## Something else is not working

Please open a new issue

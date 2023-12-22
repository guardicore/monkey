import os

feature_flags = os.environ.get("FEATURE_FLAGS", "")
NEXT_JS_UI_FEATURE = feature_flags.find("NEXT_JS_UI") != -1

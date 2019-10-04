# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import markdown
import base64

def main(params):
    try:
        text = params["markdown"]
    except:
        return {'Error' : 'Possibly lacking markdown parameter in request.'}

    decoded_text = base64.b64decode(text.encode()).decode()

    html = markdown.markdown(decoded_text)

    return {"html_response": html}

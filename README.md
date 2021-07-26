# qbittorrent-k8s-controller
A super simple controller for chrisjohnson00/qbittorrent-openvpn 

## Dependencies

    pip install --upgrade pip
    pip install --upgrade pygogo kubernetes
    pip freeze > requirements.txt
    sed -i '/pkg_resources/d' requirements.txt


## Env vars

  - `KILL_AFTER_RESTARTS` - How many times the pod must be restarted before it is deleted
  - `NAMESPACE` - The namespace to look for pods within
  - `LABEL_SELECTOR` - The label selector to select pods with, for example: `app=qbittorrent`

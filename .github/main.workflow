workflow "build and push image" {
  on = "push"
  resolves = ["one-click-docker-marketplace"]
}

action "one-click-docker-marketplace" {
  uses = "pangzineng/Github-Action-One-Click-Docker@master"
  secrets = [
    "DOCKER_NAMESPACE",
    "DOCKER_PASSWORD",
    "DOCKER_USERNAME",
    "DOCKER_REGISTRY_URL",
    "MARKETPLACE_DEFINITIONS",
    "MARKETPLACE_KEYWORD",
    "MARKETPLACE_CUSTOM_KEY",
  ]
  args = "--build-arg DEFINITIONS=\"$MARKETPLACE_DEFINITIONS\" --build-arg SERVICE_NAME=\"$MARKETPLACE_KEYWORD\" --build-arg CUSTOM_KEY=\"$MARKETPLACE_CUSTOM_KEY\" ."
  env = {
    BRANCH_FILTER = "master"
    DOCKER_TAG_APPEND = "$MARKETPLACE_KEYWORD"
  }
}

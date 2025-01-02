job "JOB_NAME_FOR_SYSTEM" {
  
  datacenters = ["dc1"]
  type        = "service"  # or system / batch / sysbatch
  priority    = 50
  
  meta {
    version = "1.0.0"
    environment = "production"
    team = "backend"
    project = "general"
    deploy_method = "standard"
    monitoring_url = "none"
    git_repo = "https://bitbucket.org/safebytelabs/mypkg"
  }
  
  group "infra" {

    # This parameter affects the autoscaling options
    count = 1

    # Configures network resources
    network {
      port "SERVICENAME-PROTOCOL" {
        to = PORTNUMBER  # or static = PORTNUMBER
      }    
    }

    # Configures how this service appears in Consul
    service {
      name = "SERVICENAME-PROTOCOL"
      port = "SERVICENAME-PROTOCOL"
      check {
        name     = "PROTOCOL alive"
        type     = "tcp"
        interval = "60s"
        timeout  = "2s"
      }
    }

    # Configures what exactly to execute
    task "SERVICENAME" {
      driver = "docker"

      # Environment variables for the container
      env {}

      # Log retention for the container
      logs {
        max_files     = 10
        max_file_size = 10
      }

      # Sets a top/max limit on resource consumption
      resources {
        cpu    = 100
        memory = 256
      }

      # Container details
      config {
        image = "CONTAINERNAME:CONTAINERVERSION"
        ports = ["SERVICENAME-PROTOCOL"]
        args = []
        volumes = [
           "custom/default.conf:/etc/service/default.conf",
        ]        
      }  

# --- TEMPLATE STARTS ---
    template {
      data = <<EOH
[...]
EOH 
      destination = "custom/default.conf"
    }      
# --- TEMPLATE ENDS ---

    } # task
  } # group
} # job

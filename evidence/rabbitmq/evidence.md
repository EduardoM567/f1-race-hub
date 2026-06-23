#rabbitmq 

##What I did
Set up RabbitMQ centralized logging system

##What exists
-Log_queue created
-Log_queeue_dlq created
-Log_exchange created

##what works
-RabbitMQ UI opens in browser
-Queues show in dashboard
-DLQ structure is configured

##Notes
this system sends logs to a main queue and routes bad messages to DLQ

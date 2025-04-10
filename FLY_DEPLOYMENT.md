# Deploying to Fly.io (Development Environment)

This guide walks you through deploying your Django Tenants + Vue.js application to Fly.io as a minimal development environment.

## Prerequisites

1. Install the Fly CLI:
   ```bash
   # On Windows with PowerShell
   iwr https://fly.io/install.ps1 -useb | iex
   
   # On macOS or Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. Login to Fly.io:
   ```bash
   fly auth login
   ```

3. Ensure your database is properly configured. The application currently uses NeonDB as per the settings file.

## Deployment Steps for Development

1. Create your Fly.io app:
   ```bash
   fly apps create fspapplication
   ```

2. Create a smaller volume for development data:
   ```bash
   cd /mnt/f/Fsp\ Application/
   fly volumes create fspapplication_data --size 1 --region syd -a fspapplication
   ```

3. Deploy your application with minimal resources:
   ```bash
   fly deploy -a fspapplication
   ```

   > Note: All environment variables are already included in the fly.toml file for development purposes. For production, you should use `fly secrets set` instead.

4. Open your application:
   ```bash
   fly open
   ```

## Cost-Saving Features

This deployment includes several cost-saving features:

1. **Scale to Zero**: The application is configured to scale down to zero when not in use with `min_machines_running = 0`
2. **Minimal Resource Usage**: Using only 256MB of RAM and 1 shared CPU
3. **Optimized Docker Image**: Alpine and slim base images to reduce storage costs
4. **Minimal Workers**: Gunicorn is configured with just 2 workers and 2 threads

## Monitoring Costs

To monitor your usage and costs:

```bash
fly status
fly dashboard
```

## Updating Your Application

To update your development application after making changes:

```bash
fly deploy
```

## Managing the Application

### Starting/Stopping 

If you need to manually stop the application to save resources:

```bash
fly scale count 0
```

To restart it:

```bash
fly scale count 1
```

### Important Notes

- With `min_machines_running = 0`, your application will shut down after 5 minutes of inactivity
- The first request after inactivity will cause a cold start (might take 15-30 seconds)
- This configuration is optimized for development, not production use

## Troubleshooting

If you encounter issues with the deployment:

1. Check the application logs:
   ```bash
   fly logs
   ```

2. Connect to a running instance to debug:
   ```bash
   fly ssh console
   ```

3. If you need more resources for specific tasks, you can temporarily scale up:
   ```bash
   fly scale memory 512
   # And scale back down when done
   fly scale memory 256
   ```

## Additional Configuration

### Database Connection

If you need to connect to an external PostgreSQL database, make sure the database connection string is properly set up in your Django settings.

### Custom Domain

To set up a custom domain for your application:

```bash
fly certs create your-domain.com
```

### SSL Certificate

Fly.io automatically manages SSL certificates for your application.

### Monitoring

You can use the Fly.io dashboard to monitor your application's performance and health. 
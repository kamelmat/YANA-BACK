# GitHub Actions Pipeline Documentation: Deploy React to GCP

## Overview
This GitHub Actions pipeline automates the build and deployment of a Vite-based React frontend application to a Google Cloud Storage (GCS) bucket. The pipeline is triggered on pushes to the `main` branch or manually via workflow dispatch. It consists of two jobs: `build` and `deploy`, which handle the compilation of the React application and its deployment to GCS, respectively.

## Pipeline Metadata
- **Name**: Deploy React to GCP
- **Concurrency**:
  - **Group**: `${{ github.workflow }}-${{ github.ref }}`
  - **Cancel-in-progress**: `true`
  - **Purpose**: Ensures only one instance of the pipeline runs for a given branch, canceling any in-progress runs for the same branch to avoid conflicts.
- **Triggers**:
  - **Push**: Runs on pushes to the `main` branch.
  - **Workflow Dispatch**: Allows manual triggering from the GitHub Actions UI.

## Environment Variables
The following global environment variables are defined at the pipeline level:
- `NODE_VERSION`: Specifies the Node.js version (`20.x`) used for building the application.
- `PROJECT_ID`: The Google Cloud project ID (`training-batch-05`) where the GCS bucket resides.
- `GCS_BUCKET`: The target GCS bucket (`gs://yana-front`) for deploying the built artifacts.

## Jobs

### 1. Build Job
- **Name**: Build Vite React App
- **Runner**: `ubuntu-latest`
- **Purpose**: Compiles the Vite-based React application and prepares the build artifacts for deployment.
- **Steps**:
  1. **Checkout Repository**:
     - **Action**: `actions/checkout@v4`
     - **Description**: Clones the repository to the runner, ensuring the latest code is available for building.
  2. **Setup Node.js**:
     - **Action**: `actions/setup-node@v4`
     - **Configuration**:
       - `node-version`: Uses the `NODE_VERSION` environment variable (`20.x`).
       - `check-latest`: Ensures the latest patch version of Node.js is used.
     - **Description**: Configures the Node.js environment for the specified version.
  3. **Cache Dependencies**:
     - **Action**: `actions/cache@v4`
     - **Configuration**:
       - `path`: Caches `node_modules` and `~/.npm` to speed up subsequent runs.
       - `key`: Generated based on the OS and the hash of `package-lock.json` to ensure cache consistency.
       - `restore-keys`: Allows fallback to previous caches if the exact key is not found.
     - **Description**: Caches npm dependencies to reduce installation time in future runs.
  4. **Install Dependencies**:
     - **Command**: `npm ci --prefer-offline --no-audit`
     - **Environment**:
       - `CI: true` - Optimizes npm for CI environments, skipping interactive prompts.
     - **Description**: Installs project dependencies using `npm ci`, which ensures a clean and reproducible installation based on `package-lock.json`.
  5. **Build Project**:
     - **Command**: `npm run build`
     - **Environment**:
       - `CI: true` - Ensures Vite treats the build as a CI process, failing on warnings if configured.
     - **Description**: Runs the Vite build script to compile the React application, generating optimized static assets in the `dist` directory.
  6. **Upload Build Artifacts**:
     - **Action**: `actions/upload-artifact@v4`
     - **Configuration**:
       - `name`: `dist`
       - `path`: `./dist`
     - **Description**: Uploads the `dist` directory as an artifact, making it available for the `deploy` job.

### 2. Deploy Job
- **Name**: Deploy Vite React App to GCP
- **Runner**: `ubuntu-latest`
- **Dependencies**: Requires the `build` job to complete successfully (`needs: build`).
- **Purpose**: Deploys the built artifacts to the specified GCS bucket and configures caching headers.
- **Steps**:
  1. **Checkout Repository**:
     - **Action**: `actions/checkout@v4`
     - **Description**: Clones the repository to ensure access to any scripts or configuration needed during deployment.
  2. **Download Build Artifacts**:
     - **Action**: `actions/download-artifact@v4`
     - **Configuration**:
       - `name`: `dist`
       - `path`: `./dist`
     - **Description**: Downloads the `dist` artifact produced by the `build` job to the runner.
  3. **Authenticate to Google Cloud**:
     - **Action**: `google-github-actions/auth@v2`
     - **Configuration**:
       - `credentials_json`: Uses the `GCP_SA_KEY` secret, which contains the Service Account key for authentication.
     - **Description**: Authenticates the runner with Google Cloud, enabling access to GCS and other GCP services.
  4. **Upload to GCS Bucket**:
     - **Command**:
       ```bash
       gsutil -m rsync -r -d ./dist ${{ env.GCS_BUCKET }}
       gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" ${{ env.GCS_BUCKET }}/**/*.js
       gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" ${{ env.GCS_BUCKET }}/**/*.css
       gsutil -m setmeta -h "Cache-Control:no-cache" ${{ env.GCS_BUCKET }}/index.html
       ```
     - **Description**:
       - Synchronizes the `dist` directory with the GCS bucket, deleting any files in the bucket that are not in `dist`.
       - Sets a long cache duration (1 year) for JavaScript and CSS files to improve performance.
       - Disables caching for `index.html` to ensure users always receive the latest version.

## Secrets
The pipeline relies on the following GitHub secret:
- `GCP_SA_KEY`: A JSON key for a Google Cloud Service Account with permissions to write to the specified GCS bucket and (if enabled) invalidate Cloud CDN caches.

## Prerequisites
- A Vite-based React project with a `build` script that generates static assets in the `dist` directory.
- A Google Cloud project (`training-batch-05`) with a GCS bucket (`gs://yana-front`) configured for static website hosting.
- A Google Cloud Service Account with appropriate permissions and its key stored as a GitHub secret (`GCP_SA_KEY`).
- Node.js version `20.x` compatible with the project dependencies.

## Usage
1. **Automatic Trigger**: Push changes to the `main` branch to trigger the pipeline.
2. **Manual Trigger**: Use the GitHub Actions UI to trigger the pipeline via "Run workflow."
3. **Monitoring**: Check the pipeline's progress and logs in the GitHub Actions tab of the repository.
4. **Verification**: After deployment, verify that the updated application is accessible via the GCS bucket's public URL or associated CDN.

## Notes
- **Caching Strategy**: The pipeline sets aggressive caching for JavaScript and CSS files (`max-age=31536000`) to optimize performance, while `index.html` is set to `no-cache` to ensure immediate updates.
- **Concurrency Control**: The `concurrency` setting prevents multiple simultaneous deployments, which could lead to inconsistent states in the GCS bucket.
- **Extensibility**: To support environment variables in the frontend, consider adding `VITE_*` variables to the `build` job's environment and configuring Vite to include them in the bundle (see Vite documentation for details).

## Troubleshooting
- **Build Failures**: Check the `npm run build` logs for errors related to code or dependencies. Ensure `package-lock.json` is up-to-date.
- **Deployment Failures**: Verify the `GCP_SA_KEY` secret is valid and the Service Account has write access to the GCS bucket.
- **Caching Issues**: If users see outdated content, ensure `index.html` is set to `no-cache` and consider enabling the CDN cache invalidation step.
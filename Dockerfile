# Simple two-stage build to avoid Nixpacks' node_modules/.cache mount clash
# (npm ci fails with EBUSY on rmdir /app/node_modules/.cache).
FROM node:20-alpine AS build
WORKDIR /app

# git is needed at build time so scripts/build.mjs can read commit history
RUN apk add --no-cache git

COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

# Copy the full repo — the build script reads STATUS.md, board/, ciphers/, etc.
COPY . .

# Railway's build context carries no .git, but the site is built from history
# (activity, replay, the draw's idle clocks). The repo is public, so fetch it.
# RAILWAY_GIT_COMMIT_SHA pins the fetch to the commit being deployed. If the
# fetch fails the build still succeeds and the site says it has no history.
ARG RAILWAY_GIT_COMMIT_SHA
RUN if [ ! -e .git ]; then \
      git init -q . \
      && git remote add origin https://github.com/AlexFitzgerald47/cracking-problems-hub.git \
      && git fetch -q origin "${RAILWAY_GIT_COMMIT_SHA:-main}" \
      && git reset -q --soft FETCH_HEAD \
      || echo "WARNING: could not fetch git history; building without it"; \
    fi

RUN npm run build

FROM node:20-alpine AS run
WORKDIR /app
ENV NODE_ENV=production

COPY --from=build /app/package.json /app/package-lock.json ./
RUN npm ci --omit=dev --no-audit --no-fund && npm cache clean --force

COPY --from=build /app/dist ./dist
COPY --from=build /app/server.mjs ./server.mjs

EXPOSE 8080
CMD ["node", "server.mjs"]

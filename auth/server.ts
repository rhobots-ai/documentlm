import express from "express";
import cors from "cors";
import { fromNodeHeaders, toNodeHandler } from "better-auth/node";
import { auth } from "./lib/auth.ts";
import config from './config.ts';

const app = express();
const port = config.PORT;

// CORS configuration - moved to the top
app.use(cors({
  origin: config.TRUSTED_ORIGINS,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

// Debugging middleware - log all incoming requests
// app.use((req, res, next) => {
//   console.log(`Incoming ${req.method} request to ${req.path}`);
//   console.log('Headers:', req.headers);
//   next();
// });

app.options('{*any}', (req, res) => {
  res.sendStatus(204);
});

// Your auth route
app.all("/api/auth/{*any}", (req, res, next) => {
  const handler = toNodeHandler(auth);
  handler(req, res, next);
});

// Other middleware and routes
app.use(express.json());

app.get("/api/me", async (req: any, res: any) => {
  const session = await auth.api.getSession({
    headers: fromNodeHeaders(req.headers),
  });
  return res.json(session);
});

app.listen(port, () => {
  console.log(`Better Auth app listening on port ${port}`);
});
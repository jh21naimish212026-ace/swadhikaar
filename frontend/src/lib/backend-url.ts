const LOCAL_BACKEND_DEFAULT = "http://localhost:8000";

function normalizeUrl(value?: string | null): string {
  return (value || "").trim().replace(/\/$/, "");
}

export function getBackendUrl(): string {
  const configured = normalizeUrl(process.env.NEXT_PUBLIC_BACKEND_URL);
  if (configured) return configured;

  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return (
        normalizeUrl(process.env.NEXT_PUBLIC_BACKEND_FALLBACK_URL) ||
        LOCAL_BACKEND_DEFAULT
      );
    }
  }

  return "";
}

export function backendUrlErrorMessage(): string {
  return "Backend URL not configured. Set NEXT_PUBLIC_BACKEND_URL to a public API URL.";
}

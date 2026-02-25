function extract_user_id(r) {
  var auth = r.headersIn.Authorization;

  // If no Authorization header is present
  if (!auth) {
    return "anonymous";
  }

  var token = auth.split(" ")[1];

  if (!token) {
    return "anonymous";
  }

  var parts = token.split(".");

  // JWT must have three parts
  if (parts.length !== 3) {
    return "anonymous";
  }

  try {
    // Decode JWT payload (base64)
    var payload = JSON.parse(Buffer.from(parts[1], "base64").toString());

    // Return subject claim if exists
    return payload.sub || "anonymous";
  } catch (e) {
    return "anonymous";
  }
}

export default { extract_user_id };

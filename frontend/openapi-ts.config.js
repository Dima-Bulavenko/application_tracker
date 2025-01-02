import {  defaultPlugins } from "@hey-api/openapi-ts";
import { defineConfig, } from "./plugins/zod";

export default {
    client: "@hey-api/client-axios",
    experimentalParser: true, // For OpenAPI 3.0 or newer, also needed for zod validation
    input: "openapi.json",
    output: {
        path:"src/client",
        format: 'prettier',
    },
    plugins: [
        ...defaultPlugins,
        defineConfig(),
    ],
};

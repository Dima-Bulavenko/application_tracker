import type { Plugin, OpenApiV3_0_X } from "@hey-api/openapi-ts";
import type { Config } from "./types";
import $RefParser from "@apidevtools/json-schema-ref-parser";
import { jsonSchemaToZod, Options, JsonSchema } from "json-schema-to-zod";

export const handler: Plugin.Handler<Config> = async ({ context, plugin }) => {
    const schemas = (
        (await $RefParser.dereference(context.spec)) as OpenApiV3_0_X
    ).components?.schemas;

    const file = context.createFile({
        id: plugin.name,
        path: plugin.output,
    });

    const options: Options = {
        module: "esm",
        noImport: true,
    };
    file.import({
        module: "zod",
        name: "z",
    });
    for (const key in schemas) {
        options.name = `z${key}`;
        const code = jsonSchemaToZod(schemas[key] as JsonSchema, options);
        file.add(code);
    }
};

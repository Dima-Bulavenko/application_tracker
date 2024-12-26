import { zodResolver, Resolver } from "@hookform/resolvers/zod";
import { FieldValues, ResolverOptions, ResolverResult } from "react-hook-form";

export const customZodResolver: Resolver = (
    schema,
    schemaOptions,
    resolverOptions = {}
) => {
    return async <TFieldValues extends FieldValues, TContext>(
        values: TFieldValues,
        context: TContext | undefined,
        options: ResolverOptions<TFieldValues>
    ): Promise<ResolverResult<TFieldValues>> => {
        // Transform the values, with the result being of type Transform<TFieldValues>
        const transformedValues = transformValues(
            values
        ) as unknown as TFieldValues;

        // Pass transformed values to the original zodResolver
        return zodResolver(schema, schemaOptions, resolverOptions)(
            transformedValues,
            context,
            options
        );
    };
};

type Transform<T> = T extends string
    ? string | undefined
    : T extends FieldValues
    ? { [K in keyof T]: Transform<T[K]> }
    : T extends unknown[]
    ? Transform<T[number]>[]
    : T;

function transformValues<T extends FieldValues | unknown[]>(
    values: T
): Transform<T> {
    const transformedValues = Array.isArray(values) ? [] : {};
    for (const key in values) {
        const value = values[key];
        (transformedValues as Record<string, unknown>)[key] =
            typeof value === "string"
                ? value.trim() || undefined
                : typeof value === "object" && value !== null
                ? transformValues(value)
                : value;
    }
    return transformedValues as Transform<T>;
}

import { z } from "zod";
import { useForm, useController, UseControllerProps } from "react-hook-form";
import { TextField } from "@mui/material";
import { ApplicationCreateDto } from "./client/types.gen";
import {zApplicationCreateDTO} from './client/zod.gen' 

import { customZodResolver } from "./utils/customZodResolver";

function Input(props: UseControllerProps<ApplicationCreateDto>) {
    const { field, fieldState } = useController(props);
    return (
        <>
            <TextField
                {...field}
                value={field.value || ""}
                placeholder={props.name}
                helperText={fieldState.error ? fieldState.error?.message : ""}
                error={Boolean(fieldState.error)}
            />
        </>
    );
}

export default function App() {
    const { handleSubmit, control } = useForm<ApplicationCreateDto>({
        resolver: customZodResolver(zApplicationCreateDTO),
    });
    const zodString = z.string().optional();
    console.log(zodString.parse(""));

    const onSubmit = (data: ApplicationCreateDto) => console.log(data);
    return (
        <>
            <form onSubmit={handleSubmit(onSubmit)}>
                <Input control={control} name="role" />
                <Input control={control} name="work_type" />
                <Input control={control} name="work_location" />
                <Input control={control} name="application_url" />
                <Input control={control} name="notes" />
                <Input control={control} name="interview_date" />
                {/* <Input control={control} name="company" /> */}
                <input type="submit" value="submit" />
            </form>
        </>
    );
}

class BaseTool:
    name = ""
    description = ""
    schema = None  # Pydantic model

    def get_schema_text(self):
        fields = self.schema.model_fields

        schema_str = ""
        for field_name, field in fields.items():
            field_type = str(field.annotation)

            schema_str += f"- {field_name}: {field_type}\n"

        return schema_str

    def generate_prompt(self, config, user_prompt):
        raise NotImplementedError

    def execute(self, actions, operation):
        raise NotImplementedError
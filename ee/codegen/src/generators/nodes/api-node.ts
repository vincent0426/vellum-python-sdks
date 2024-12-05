import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { isNil } from "lodash";

import { ApiNodeContext } from "src/context/node-context/api-node";
import { NodeInput } from "src/generators";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { ApiNode as ApiNodeType, ConstantValuePointer } from "src/types/vellum";

export class ApiNode extends BaseSingleFileNode<ApiNodeType, ApiNodeContext> {
  baseNodeClassName = "APINode";
  baseNodeDisplayClassName = "BaseAPINodeDisplay";

  getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    const urlInput = this.nodeInputsByKey.get("url");
    if (!urlInput) {
      throw new Error('Node input "url" is required but not found.');
    }

    statements.push(
      python.field({
        name: "url",
        initializer: urlInput,
      })
    );

    statements.push(
      python.field({
        name: "method",
        initializer: this.convertMethodValueToEnum(),
      })
    );

    const body = this.nodeInputsByKey.get("body");

    if (body) {
      statements.push(
        python.field({
          name: "json",
          initializer: body,
        })
      );
    }

    if (this.nodeData.data.additionalHeaders) {
      statements.push(
        python.field({
          name: "headers",
          initializer: python.TypeInstantiation.dict(
            this.nodeData.data.additionalHeaders.map((header) => {
              const keyInput = this.nodeData.inputs.find(
                (input) => input.id === header.headerKeyInputId
              );
              const valueInput = this.nodeData.inputs.find(
                (input) => input.id === header.headerValueInputId
              );

              if (!keyInput || !valueInput) {
                throw new Error(
                  `Input not found for header: ${JSON.stringify(header)}`
                );
              }
              const key = new NodeInput({
                workflowContext: this.workflowContext,
                nodeInputData: keyInput,
              });
              const value = new NodeInput({
                workflowContext: this.workflowContext,
                nodeInputData: valueInput,
              });

              return {
                key: key,
                value: value,
              };
            })
          ),
        })
      );
    }

    if (this.nodeData.data.apiKeyHeaderKeyInputId) {
      statements.push(
        python.field({
          name: "api_key_header_key",
          initializer: python.TypeInstantiation.str(
            this.nodeData.data.apiKeyHeaderKeyInputId
          ),
        })
      );
    }

    if (this.nodeData.data.authorizationTypeInputId) {
      const authInput = this.nodeData.inputs.find(
        (input) => input.id === this.nodeData.data.authorizationTypeInputId
      );
      if (!authInput) {
        throw new Error(
          `No inputs have authorization type id of ${this.nodeData.data.authorizationTypeInputId}`
        );
      }
      const value = this.nodeInputsByKey.get(authInput.key);
      if (!value) {
        throw new Error(`No inputs have key of ${authInput.key}`);
      }
      statements.push(
        python.field({
          name: "authorization_type",
          initializer: value,
        })
      );
    }

    if (this.nodeData.data.apiKeyHeaderValueInputId) {
      const valueInput = this.nodeData.inputs.find(
        (input) => input.id === this.nodeData.data.apiKeyHeaderValueInputId
      );
      if (!valueInput) {
        throw new Error(
          `No inputs have api header value id of ${this.nodeData.data.apiKeyHeaderValueInputId}`
        );
      }
      const value = this.nodeInputsByKey.get(valueInput.key);
      if (!value) {
        throw new Error(`No inputs have key of ${valueInput.key}`);
      }
      statements.push(
        python.field({
          name: "api_key_header_value",
          initializer: value,
        })
      );
    }

    if (this.nodeData.data.bearerTokenValueInputId) {
      const valueInput = this.nodeData.inputs.find(
        (input) => input.id === this.nodeData.data.bearerTokenValueInputId
      );
      if (!valueInput) {
        throw new Error(
          `No inputs have bearer token header value id of ${this.nodeData.data.bearerTokenValueInputId}`
        );
      }
      const value = this.nodeInputsByKey.get(valueInput.key);
      if (!value) {
        throw new Error(`No inputs have key of ${valueInput.key}`);
      }
      statements.push(
        python.field({
          name: "bearer_token_value",
          initializer: value,
        })
      );
    }

    return statements;
  }

  getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    if (!isNil(this.nodeData.data.urlInputId)) {
      statements.push(
        python.field({
          name: "url_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.urlInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.methodInputId)) {
      statements.push(
        python.field({
          name: "method_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.methodInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.bodyInputId)) {
      statements.push(
        python.field({
          name: "body_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.bodyInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.authorizationTypeInputId)) {
      statements.push(
        python.field({
          name: "authorization_type_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.authorizationTypeInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.bearerTokenValueInputId)) {
      statements.push(
        python.field({
          name: "bearer_token_value_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.bearerTokenValueInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.apiKeyHeaderKeyInputId)) {
      statements.push(
        python.field({
          name: "api_key_header_key_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.apiKeyHeaderKeyInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.apiKeyHeaderValueInputId)) {
      statements.push(
        python.field({
          name: "api_key_header_value_input_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.apiKeyHeaderValueInputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.textOutputId)) {
      statements.push(
        python.field({
          name: "text_output_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.textOutputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.jsonOutputId)) {
      statements.push(
        python.field({
          name: "json_output_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.jsonOutputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.statusCodeOutputId)) {
      statements.push(
        python.field({
          name: "status_code_output_id",
          initializer: python.TypeInstantiation.uuid(
            this.nodeData.data.statusCodeOutputId
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.additionalHeaders)) {
      statements.push(
        python.field({
          name: "additional_header_key_input_ids",
          initializer: python.TypeInstantiation.dict(
            this.nodeData.data.additionalHeaders.map((header) => {
              const nodeInput = this.nodeData.inputs.find(
                (nodeInput) => nodeInput.id === header.headerValueInputId
              );

              if (!nodeInput) {
                throw new Error(
                  `Node input with ID ${header.headerValueInputId} not found`
                );
              }

              return {
                key: python.TypeInstantiation.str(nodeInput.key),
                value: python.TypeInstantiation.uuid(nodeInput.id),
              };
            })
          ),
        })
      );
    }

    if (!isNil(this.nodeData.data.additionalHeaders)) {
      statements.push(
        python.field({
          name: "additional_header_value_input_ids",
          initializer: python.TypeInstantiation.dict(
            this.nodeData.data.additionalHeaders.map((header) => {
              const nodeInput = this.nodeData.inputs.find(
                (nodeInput) => nodeInput.id === header.headerValueInputId
              );

              if (!nodeInput) {
                throw new Error(
                  `Node input with ID ${header.headerValueInputId} not found`
                );
              }

              return {
                key: python.TypeInstantiation.str(nodeInput.key),
                value: python.TypeInstantiation.uuid(nodeInput.id),
              };
            })
          ),
        })
      );
    }

    return statements;
  }

  protected getOutputDisplay(): python.Field {
    return python.field({
      name: "output_display",
      initializer: python.TypeInstantiation.dict(
        // TODO: Specify output displays
        //    https://app.shortcut.com/vellum/story/5640
        []
      ),
    });
  }

  getErrorOutputId(): string | undefined {
    return this.nodeData.data.errorOutputId;
  }

  private convertMethodValueToEnum(): AstNode {
    const methodValue = this.nodeData.inputs
      .find((input) => input.id === this.nodeData.data.methodInputId)
      ?.value.rules.find(
        (value) => value.type === "CONSTANT_VALUE"
      ) as ConstantValuePointer;

    if (!methodValue) {
      throw new Error(
        `No method input found for input id ${this.nodeData.data.methodInputId} and of type "CONSTANT_VALUE"`
      );
    }

    const methodEnum = methodValue.data.value as string;

    return python.reference({
      name: "APIRequestMethod",
      modulePath: [
        ...this.workflowContext.sdkModulePathNames.WORKFLOWS_MODULE_PATH,
        "constants",
      ],
      attribute: [methodEnum],
    });
  }
}

import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { ErrorNode } from "src/types/vellum";

export class ErrorNodeContext extends BaseNodeContext<ErrorNode> {
  baseNodeClassName = "ErrorNode";
  baseNodeDisplayClassName = "BaseErrorNodeDisplay";
  isCore = true;

  getNodeOutputNamesById(): Record<string, string> {
    return {
      [this.nodeData.data.errorOutputId]: "error",
    };
  }

  createPortContexts(): PortContext[] {
    return [];
  }
}

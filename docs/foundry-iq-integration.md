# Foundry IQ Integration Guide

This project is wired for Microsoft Foundry Agent Service plus Foundry IQ. Local fallback retrieval is included for demos before cloud resources are configured.

## What To Create In Microsoft Foundry

1. Create a Microsoft Foundry project.
2. Deploy a model supported by Foundry Agent Service.
3. Create a Foundry Agent Service agent named `JEE Mentor AI`.
4. Create a Foundry IQ knowledge base named `jee-mentor-knowledge`.
5. Add a knowledge source for JEE notes, formulas, solved examples, and concept explanations.
6. Connect the Foundry IQ knowledge base to the agent through the documented MCP knowledge-base connection.
7. Prefer extractive data output mode for agent integration so the API can show citations.

Microsoft Learn references:

- [What is Foundry IQ?](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq)
- [Connect a Foundry IQ knowledge base to Foundry Agent Service](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/foundry-iq-connect?view=foundry)
- [Build with agents, conversations, and responses in Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/runtime-components)

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill:

```bash
FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
FOUNDRY_AGENT_ID=<agent-id>
FOUNDRY_IQ_ENDPOINT=<knowledge-base-api-endpoint>
FOUNDRY_IQ_API_KEY=<key>
FOUNDRY_IQ_KNOWLEDGE_BASE_ID=<knowledge-base-id>
```

## Knowledge Content

Start with the markdown files in `knowledge-base/`. Upload these to the Foundry IQ source or store them in Azure Blob Storage and connect the blob container as the indexed knowledge source.

Recommended content groups:

- Formula sheets by subject.
- Topic notes with common mistakes.
- Solved JEE Main and Advanced examples.
- Short concept explanations for retrieval.
- Metadata: `subject`, `topic`, `difficulty`, `exam_type`, and `source`.

## Backend Behavior

`KnowledgeService.retrieve()` first calls Foundry IQ when all Foundry IQ variables are present. If that call fails or variables are missing, it falls back to local markdown retrieval so the app remains demoable.

`JeeMentorAgent.solve()` first calls the configured Foundry Agent Service agent. If cloud execution is unavailable, it returns a deterministic local tutoring response that keeps the UI and analytics working.

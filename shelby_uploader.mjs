import "dotenv/config.js";
import fs from "fs";
import { Account, Ed25519PrivateKey, Network } from "@aptos-labs/ts-sdk";
import { ShelbyNodeClient } from "@shelby-protocol/sdk/node";

async function main() {
    try {
        const args = process.argv.slice(2);
        if (args.length < 2) {
            console.error(JSON.stringify({ success: false, error: "Missing required arguments: <file_path> <blob_name>" }));
            process.exit(1);
        }

        const filePath = args[0];
        const blobName = args[1];

        const { SHELBY_ACCOUNT_ADDRESS, SHELBY_ACCOUNT_PRIVATE_KEY, SHELBY_API_KEY, SHELBY_NETWORK } = process.env;

        if (!SHELBY_ACCOUNT_PRIVATE_KEY || !SHELBY_API_KEY) {
            console.error(JSON.stringify({ success: false, error: "Environment variables SHELBY_ACCOUNT_PRIVATE_KEY and SHELBY_API_KEY must be set." }));
            process.exit(1);
        }

        const networkMap = {
            "mainnet": Network.MAINNET,
            "testnet": Network.TESTNET,
            "devnet": Network.DEVNET,
            "shelbynet": Network.SHELBYNET
        };
        const currentNetwork = networkMap[(SHELBY_NETWORK || "shelbynet").toLowerCase()] || Network.SHELBYNET;

        const client = new ShelbyNodeClient({
            network: currentNetwork,
            apiKey: SHELBY_API_KEY,
        });

        const signer = Account.fromPrivateKey({
            privateKey: new Ed25519PrivateKey(SHELBY_ACCOUNT_PRIVATE_KEY),
        });


        const duration = 30 * 24 * 60 * 60 * 1000000;
        const expirationMicros = Date.now() * 1000 + duration;

        const blobData = fs.readFileSync(filePath);

        const response = await client.upload({
            blobData,
            signer,
            blobName,
            expirationMicros,
        });

        console.error("DEBUG:", response);

        console.log(JSON.stringify({
            success: true,
            blob_id: blobName,
            url: `https://explorer.shelby.xyz/shelbynet/account/${SHELBY_ACCOUNT_ADDRESS}`,
            error: null
        }));

    } catch (e) {
        console.error(JSON.stringify({
            success: false,
            blob_id: null,
            url: null,
            error: e.message || String(e)
        }));
        process.exit(1);
    }
}

main();

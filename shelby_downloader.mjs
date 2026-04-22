import "dotenv/config.js";
import fs from "fs";
import { Readable } from "stream";
import { pipeline } from "stream/promises";
import { AccountAddress, Network } from "@aptos-labs/ts-sdk";
import { ShelbyNodeClient } from "@shelby-protocol/sdk/node";

async function main() {
    try {
        const args = process.argv.slice(2);
        if (args.length < 2) {
            console.error(JSON.stringify({ success: false, error: "Missing blob_name and output_path arguments" }));
            process.exit(1);
        }
        const blobName = args[0];
        const outPath = args[1];

        const { SHELBY_ACCOUNT_ADDRESS, SHELBY_API_KEY, SHELBY_NETWORK } = process.env;
        if (!SHELBY_ACCOUNT_ADDRESS || !SHELBY_API_KEY) {
            console.error(JSON.stringify({ success: false, error: "Missing config keys in .env" }));
            process.exit(1);
        }

        const networkMap = { 
            mainnet: Network.MAINNET, 
            testnet: Network.TESTNET, 
            devnet: Network.DEVNET, 
            shelbynet: Network.SHELBYNET 
        };
        const currentNetwork = networkMap[(SHELBY_NETWORK || "shelbynet").toLowerCase()] || Network.SHELBYNET;

        const client = new ShelbyNodeClient({ network: currentNetwork, apiKey: SHELBY_API_KEY });
        const account = AccountAddress.fromString(SHELBY_ACCOUNT_ADDRESS);

        const blob = await client.download({ account, blobName });
        const webStream = blob.readable;
        await pipeline(Readable.fromWeb(webStream), fs.createWriteStream(outPath));

        console.log(JSON.stringify({ 
            success: true, 
            path: outPath, 
            size: blob.contentLength ? parseInt(blob.contentLength.toString()) : null 
        }));
    } catch (e) {
        console.error(JSON.stringify({ success: false, error: e.message || String(e) }));
        process.exit(1);
    }
}
main();

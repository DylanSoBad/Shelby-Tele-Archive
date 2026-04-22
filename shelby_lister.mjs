import "dotenv/config.js";
import { AccountAddress, Network } from "@aptos-labs/ts-sdk";
import { ShelbyNodeClient } from "@shelby-protocol/sdk/node";

async function main() {
    try {
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
        
        const blobs = await client.coordination.getAccountBlobs({ account });
        
        // Map elements because some types like BigInt might crash JSON.stringify if not handled
        const blobList = blobs.map(b => ({
            name: b.name,
            size: parseInt(b.size.toString()),
            expirationMicros: parseInt(b.expirationMicros.toString())
        }));

        console.log(JSON.stringify({ success: true, blobs: blobList }));
    } catch (e) {
        console.error(JSON.stringify({ success: false, error: e.message || String(e) }));
        process.exit(1);
    }
}
main();

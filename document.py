from typing import Literal
from pydantic import BaseModel, Field


class Item(BaseModel):
    line: str
    comment: str = ""


class Card(BaseModel):
    title: str
    _orientation: Literal["horizontal", "vertical", "table"] = Field(
        default="horizontal",
        alias="orientation"
    )
    items: list[Item] = []
    sections: dict[str, list[str]] = {}  # For cards with named subsections

    class Config:
        populate_by_name = True


class Section(BaseModel):
    title: str
    subtitle: str
    cards: list[Card]


class Document(BaseModel):
    title: str = "Blockchain and Digital Assets Theme Map"
    last_revision: str = "July 21, 2026"
    url: str = "https://github.com/epogrebnyak/blockchain-theme-map"
    sections: list[Section]


# Create all sections...

document = Document(
    title="Blockchain and Digital Assets Theme Map",
    last_revision="July 21, 2026",
    url="https://github.com/epogrebnyak/blockchain-theme-map",
    sections=[
        Section(
            title="USE CASES",
            subtitle="What blockchain is useful for?",
            cards=[
                Card(
                    title="What users need blockchain for?",
                    orientation="horizontal",
                    sections={
                        "Speculative": [
                            "Spot trading (BTC, ETH, altcoins)",
                            "Memecoins",
                            "Prediction markets"
                        ],
                        "Institutional finance (CeFi)": [
                            "Payments",
                            "Exchange trading",
                            "Custody and prime brokerage",
                            "RWA issuance and trading",
                            "Derivatives"
                        ],
                        "Decentralised finance (DeFi)": [
                            "Staking (Lido, Rocket Pool)",
                            "Collateralised lending (Aave, Compound)",
                            "Exchange/AMM (Uniswap, Curve)",
                            "Derivatives (dYdX, GMX, perpetuals)",
                            "RWA protocols (MakerDAO, Centrifuge)"
                        ],
                        "Physical": [
                            "Wireless networks (Helium)",
                            "Storage (Filecoin, Arweave)",
                            "Compute (Render, Akash)",
                            "Supply chain and provenance"
                        ],
                        "Social and governance": [
                            "Identity",
                            "Reputation and credentials",
                            "Voting rights, DAOs"
                        ],
                        "Entertainment": [
                            "Gaming",
                            "Collectibles"
                        ]
                    }
                )
            ]
        ),
        Section(
            title="MINIMAL BLOCKCHAIN",
            subtitle="Core building blocks of blockchain systems",
            cards=[
                Card(
                    title="Transactions",
                    orientation="horizontal",
                    sections={
                        "Create": [
                            "Native issuance (block rewards, staking and validation)",
                            "Token minting",
                            "Airdrops and rewards"
                        ],
                        "Acquire": [
                            "At the table or P2P",
                            "Broker, ATM or card",
                            "Exchanges"
                        ],
                        "Exchange": [
                            "Centralised exchanges (CEX)",
                            "Decentralised protocols (DEX)",
                            "Aggregators",
                            "Solvers and intent-based execution",
                            "Cross-chain bridges"
                        ]
                    }
                ),
                Card(
                    title="Assets and contract types",
                    orientation="horizontal",
                    items=[
                        Item(line="Native currency (BTC, ETH, SOL)"),
                        Item(line="Stablecoins (USDC, USDT, DAI, USDe)"),
                        Item(line="Other fungible tokens (ERC-20, SPL)"),
                        Item(line="Non-fungible tokens (NFTs)"),
                        Item(line="Semi-fungible tokens"),
                        Item(line="Soulbound tokens (non-transferable)"),
                        Item(line="Off-chain data (oracles, storage proofs)")
                    ]
                ),
                Card(
                    title="Incentives",
                    orientation="horizontal",
                    items=[
                        Item(line="Fee models (gas and priority fees)"),
                        Item(line="MEV (order flow, arbitrage and liquidations)"),
                        Item(line="Staking yields and rewards"),
                        Item(line="Token supply and burn")
                    ]
                ),
                Card(
                    title="Networks",
                    orientation="horizontal",
                    items=[
                        Item(line="Bitcoin (BTC)"),
                        Item(line="Ethereum (ETH)"),
                        Item(line="L2 and L3 Rollups"),
                        Item(line="Alternative L1s (BNB, Solana, Tron)"),
                        Item(line="Private and consortium chains")
                    ]
                ),
                Card(
                    title="Foundations",
                    orientation="horizontal",
                    items=[
                        Item(line="Cryptography (hashing, digital signatures and Merkle trees)"),
                        Item(line="Address space and block data structures"),
                        Item(line="Peer-to-peer networking (node discovery and gossip protocols)"),
                        Item(line="Consensus mechanisms (participants, rules and guarantees)"),
                        Item(line="Execution environments (VMs and state transitions)"),
                        Item(line="API and user interface, account and wallet abstraction")
                    ]
                )
            ]
        ),
        Section(
            title="USER ACCESS AND CUSTODY",
            subtitle="How users and institutions hold and access assets",
            cards=[
                Card(
                    title="Wallets and key management",
                    orientation="vertical",
                    items=[
                        Item(line="Self-custodial wallets (MetaMask, Phantom, Trust Wallet)"),
                        Item(line="Smart contract wallets (Safe, Argent, Sequence)"),
                        Item(line="Account abstraction (ERC-4337, ERC-7579)"),
                        Item(line="Paymasters (gas abstraction, sponsored transactions)"),
                        Item(line="Hardware wallets (Ledger, Trezor)"),
                        Item(line="Key recovery and social recovery")
                    ]
                ),
                Card(
                    title="Institutional custody",
                    orientation="vertical",
                    items=[
                        Item(line="MPC wallets (Fireblocks, ZenGo)"),
                        Item(line="Multi-sig custody solutions"),
                        Item(line="Qualified custodians (Coinbase Custody, BitGo)"),
                        Item(line="Prime brokerage and settlement")
                    ]
                )
            ]
        ),
        Section(
            title="NETWORK ENHANCEMENTS",
            subtitle="Components that expand blockchain capabilities",
            cards=[
                Card(
                    title="Interoperability",
                    orientation="vertical",
                    items=[
                        Item(line="Bridges"),
                        Item(line="Cross-chain messaging"),
                        Item(line="Light clients")
                    ]
                ),
                Card(
                    title="Oracles and data feeds",
                    orientation="vertical",
                    items=[
                        Item(line="Price feeds (Chainlink)"),
                        Item(line="Randomness"),
                        Item(line="Cross-chain data"),
                        Item(line="Real-world event data (sports, weather and elections)"),
                        Item(line="Data aggregation and verification")
                    ]
                ),
                Card(
                    title="Storage",
                    orientation="vertical",
                    items=[
                        Item(line="On-chain storage (state and balances)"),
                        Item(line="Off-chain storage (IPFS, Arweave and Filecoin)"),
                        Item(line="Data availability layers (Celestia and EigenDA)"),
                        Item(line="Decentralized databases (Ceramic and OrbitDB)")
                    ]
                )
            ]
        ),
        Section(
            title="FEATURES AND PROTECTION",
            subtitle="Privacy, safeguards and compliance controls",
            cards=[
                Card(
                    title="Privacy and user protection",
                    orientation="vertical",
                    items=[
                        Item(line="Zero-knowledge proofs (ZK-SNARKs and ZK-STARKs)"),
                        Item(line="Stealth addresses"),
                        Item(line="Confidential transactions (hidden amounts)"),
                        Item(line="Private voting"),
                        Item(line="Encrypted metadata"),
                        Item(line="Selective disclosure (ZK-based KYC/age verification)")
                    ]
                ),
                Card(
                    title="Contract security",
                    orientation="vertical",
                    items=[
                        Item(line="Smart contract audits"),
                        Item(line="Multi-sig and custody"),
                        Item(line="Bug bounties"),
                        Item(line="Formal verification"),
                        Item(line="MEV protection")
                    ]
                ),
                Card(
                    title="Compliance",
                    orientation="vertical",
                    items=[
                        Item(line="KYC and AML"),
                        Item(line="Sanctions screening"),
                        Item(line="Transfer restrictions"),
                        Item(line="Travel rule"),
                        Item(line="Reporting and tax")
                    ]
                )
            ]
        ),
        Section(
            title="RISK MANAGEMENT",
            subtitle="Lessons and persistent risks across ecosystems",
            cards=[
                Card(
                    title="Past incidents",
                    orientation="horizontal",
                    sections={
                        "CeFi failures": [
                            "Mt. Gox (2014)",
                            "FTX (2022), Celsius (2022), BlockFi (2022)"
                        ],
                        "DeFi exploits": [
                            "The DAO (2016), Poly Network (2021), Ronin Bridge (2022), Euler Finance (2023)"
                        ],
                        "Stablecoin collapses": [
                            "Terra/LUNA (2022), USDC de-peg (2023)"
                        ],
                        "Speculative waves": [
                            "ICO boom (2017-2018)",
                            "NFT bubble (2021-2022)"
                        ],
                        "Regulatory actions": [
                            "Binance (2023-2024)",
                            "Tornado Cash (2022)"
                        ]
                    }
                )
            ]
        )
    ]
)


# Helper function to access document metadata
def get_document_info(doc: Document) -> dict:
    return {
        "title": doc.title,
        "last_revision": doc.last_revision,
        "url": doc.url,
        "total_sections": len(doc.sections),
        "total_cards": sum(len(section.cards) for section in doc.sections)
    }


# Example usage
if __name__ == "__main__":
    print(f"Document: {document.title}")
    print(f"Last revision: {document.last_revision}")
    print(f"URL: {document.url}")
    print(f"Total sections: {len(document.sections)}")
    print(f"Total cards: {sum(len(section.cards) for section in document.sections)}")

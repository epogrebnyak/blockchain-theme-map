from typing import Literal
from pydantic import BaseModel, Field


class Item(BaseModel):
    line: str
    comment: str = ""
    is_header: bool = False  # For grouping items


class Card(BaseModel):
    title: str
    orientation: Literal["horizontal", "vertical", "table"] = "horizontal"
    items: list[Item]


class Section(BaseModel):
    title: str
    subtitle: str
    cards: list[Card]


class Document(BaseModel):
    title: str = "Blockchain and Digital Assets Theme Map"
    last_revision: str = "July 21, 2026"
    url: str = "https://github.com/epogrebnyak/blockchain-theme-map"
    sections: list[Section]


# Create document
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
                    items=[
                        Item(line="Speculative", is_header=True),
                        Item(line="Spot trading (BTC, ETH, altcoins)"),
                        Item(line="Memecoins"),
                        Item(line="Prediction markets"),
                        
                        Item(line="Institutional finance (CeFi)", is_header=True),
                        Item(line="Payments"),
                        Item(line="Exchange trading"),
                        Item(line="Custody and prime brokerage"),
                        Item(line="RWA issuance and trading"),
                        Item(line="Derivatives"),
                        
                        Item(line="Decentralised finance (DeFi)", is_header=True),
                        Item(line="Staking (Lido, Rocket Pool)"),
                        Item(line="Collateralised lending (Aave, Compound)"),
                        Item(line="Exchange/AMM (Uniswap, Curve)"),
                        Item(line="Derivatives (dYdX, GMX, perpetuals)"),
                        Item(line="RWA protocols (MakerDAO, Centrifuge)"),
                        
                        Item(line="Physical", is_header=True),
                        Item(line="Wireless networks (Helium)"),
                        Item(line="Storage (Filecoin, Arweave)"),
                        Item(line="Compute (Render, Akash)"),
                        Item(line="Supply chain and provenance"),
                        
                        Item(line="Social and governance", is_header=True),
                        Item(line="Identity"),
                        Item(line="Reputation and credentials"),
                        Item(line="Voting rights, DAOs"),
                        
                        Item(line="Entertainment", is_header=True),
                        Item(line="Gaming"),
                        Item(line="Collectibles")
                    ]
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
                    items=[
                        Item(line="Create", is_header=True),
                        Item(line="Native issuance (block rewards, staking and validation)"),
                        Item(line="Token minting"),
                        Item(line="Airdrops and rewards"),
                        
                        Item(line="Acquire", is_header=True),
                        Item(line="At the table or P2P"),
                        Item(line="Broker, ATM or card"),
                        Item(line="Exchanges"),
                        
                        Item(line="Exchange", is_header=True),
                        Item(line="Centralised exchanges (CEX)"),
                        Item(line="Decentralised protocols (DEX)"),
                        Item(line="Aggregators"),
                        Item(line="Solvers and intent-based execution"),
                        Item(line="Cross-chain bridges")
                    ]
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
                    items=[
                        Item(line="CeFi failures", is_header=True),
                        Item(line="Mt. Gox (2014)"),
                        Item(line="FTX (2022), Celsius (2022), BlockFi (2022)"),
                        
                        Item(line="DeFi exploits", is_header=True),
                        Item(line="The DAO (2016), Poly Network (2021), Ronin Bridge (2022), Euler Finance (2023)"),
                        
                        Item(line="Stablecoin collapses", is_header=True),
                        Item(line="Terra/LUNA (2022), USDC de-peg (2023)"),
                        
                        Item(line="Speculative waves", is_header=True),
                        Item(line="ICO boom (2017-2018)"),
                        Item(line="NFT bubble (2021-2022)"),
                        
                        Item(line="Regulatory actions", is_header=True),
                        Item(line="Binance (2023-2024)"),
                        Item(line="Tornado Cash (2022)")
                    ]
                )
            ]
        )
    ]
)


# Helper functions
def get_document_info(doc: Document) -> dict:
    return {
        "title": doc.title,
        "last_revision": doc.last_revision,
        "url": doc.url,
        "total_sections": len(doc.sections),
        "total_cards": sum(len(section.cards) for section in doc.sections),
        "total_items": sum(
            len(card.items) 
            for section in doc.sections 
            for card in section.cards
        )
    }


def get_items_by_group(card: Card) -> dict[str, list[Item]]:
    """Group items by headers in a card"""
    groups = {}
    current_group = "Uncategorized"
    groups[current_group] = []
    
    for item in card.items:
        if item.is_header:
            current_group = item.line
            groups[current_group] = []
        else:
            groups[current_group].append(item)
    
    return groups


if __name__ == "__main__":
    print(document.model_dump_json(indent=2))

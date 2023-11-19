"""Dummy data to use in case no data is provided.
"""
EXAMPLE_DATA = [
    {
        "date": "2018-01-03",
        "type": "income",
        "amount": 94.0,
        "account": "N26",
        "category": "salary",
        "subcategory": "evotec",
        "note": "may",
    },
    {
        "date": "2018-01-02",
        "type": "income",
        "amount": 39.48,
        "account": "Wallet",
        "category": "gift",
        "subcategory": "family",
        "note": "christmas",
    },
    {
        "date": "2018-05-11",
        "type": "expense",
        "amount": -7.0,
        "account": "Wallet",
        "category": "bar",
        "subcategory": "alcohol",
        "note": "beer",
    },
    {
        "date": "2018-05-18",
        "type": "expense",
        "amount": -9.5,
        "account": "N26",
        "category": "transport",
        "subcategory": "public transport",
        "note": "bus",
    },
    {
        "date": "2018-05-11",
        "type": "expense",
        "amount": -7.0,
        "account": "Wallet",
        "category": "bar",
        "subcategory": "alcohol",
        "note": "wine",
    },
    {
        "date": "2018-05-18",
        "type": "expense",
        "amount": -9.5,
        "account": "Wallet",
        "category": "grocery",
        "subcategory": "food",
        "note": "penny",
    },
    {
        "date": "2020-12-10",
        "type": "expense",
        "amount": -50.0,
        "account": "N26",
        "category": "banktransfer",
        "subcategory": "",
        "note": "to Wallet",
    },
    {
        "date": "2020-12-16",
        "type": "income",
        "amount": 50.0,
        "account": "C24",
        "category": "banktransfer",
        "subcategory": "",
        "note": "from room",
    },
]
EXAMPLE_METADATA = {
    "accounts": ["N26", "C24", "Wallet"],
    "categories": ["salary", "gift", "bar", "transport", "grocery", "banktransfer", ""],
    "subcategories": ["food", "evotec", "family", "alcohol", "public transport", ""],
}
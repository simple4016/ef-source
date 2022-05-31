//blocknative 库配置
const Wallets = [
	{
		walletName: 'metamask',
		preferred: true
	},
	{
		walletName: 'walletConnect',
		infuraKey: '9aa3d95b3bc440fa88ea12eaa4456161',
		preferred: true
	}
]
const TTIMER = [20000, 30000]
const DappId = '48bec8e3-294f-42f5-9c94-0f657ed9db49'

let Network = 3
let Contract = {}
let HContract = {}
let API_URL = ''
let OPEN_URL = ''
let HMarkets = []
let LMarkets = []
switch (process.env.NODE_ENV) {
	// 测试环境
	case 'test':
		API_URL = 'http://api-dev.earning.farm'
		OPEN_URL = 'https://ropsten.etherscan.io/tx/'
		Network = 3
		LMarkets = ['usdc']
		HMarkets = ['usdc', 'eth']
		Contract = {
			USDC: {
				CFToken: '0xE15c9afC4DfF21707e70A976e42baa203094e362',
				ERC20DepositApprover: '0x3BF97E2284D2C1a5297536bCA9712aF69490E389',
				CFVault: '0x4BCb94F59Be87e630c4ef6414C68C631F584ACB5',
				USDC: '0xDaE821623e5bE28bD8C7994a075893290202B07b',
				Decimal: 1e6,
				Length: 2,
				Name: '稳定币去中心化收益基金',
				Introduce:
					'基于Curve的多个稳定币池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
			}
		}

		HContract = {
			USDC: {
				CFToken: '0x5de1C7CAfdBDD4faec3ef51f8C8c1A91EA20F8C0',
				CFVault: '0x47dC47921e285af62Db608f3DA7b59bdD6a74d19',
				USDC: '0x588C12309DaE98970D1Cca34d73944dD3576666A',
				CRV: '0xB0724732367C6330801B38B0a0268c890d6bA4dB',
				USDCDecimal: 1e6,
				CRVDecimal: 1e18,
				Length: 2,
				Name: '稳定币去中心化收益基金',
				Introduce:
					'基于Curve的多个稳定币池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
			},
			ETH: {
				CFToken: '0x2f47BE95129c4bA94633A06f7C2e66488D7f8d49',
				CFVault: '0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890',
				Decimal: 1e18,
				Name: 'ETH去中心化收益基金',
				Introduce:
					'基于Curve的多个ETH池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
			}
		}
		break

	// 生产环境
	case 'production':
		API_URL = 'http://api-dev.earning.farm'
		OPEN_URL = 'https://etherscan.io/tx/'
		Network = 1
		HMarkets = ['usdc', 'eth']
		LMarkets = ['usdc', 'wbtc', 'eth']
		Contract = {
			USDC: {
				CFToken: '0x412EbDc655f897e0eC0f89022bc7DEC62BAaE0aF',
				ERC20DepositApprover: '0xe5afC078684683dc232E053c2c9D86015Aa00Ec6',
				CFVault: '0x889B9194Fb1D66509d3d043e7c839582fED6E607',
				USDC: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
				Decimal: 1e6,
				Name: '稳定币去中心化收益基金',
				Introduce:
					'基于Curve的多个稳定币池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
			},
			WBTC: {
				CFToken: '0x2Eb8e7fEeC11D6dCE4799AfA3b7Bb83BbA02b081',
				ERC20DepositApprover: '0xe5afC078684683dc232E053c2c9D86015Aa00Ec6',
				CFVault: '0xAFcf9Ec311c42b4221697cf7F5392f9110DC8e8c',
				WBTC: '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
				Decimal: 1e8,
				Name: 'BTC去中心化收益基金',
				Introduce:
					'基于Curve的多个BTC ERC20池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
			},
			ETH: {
				CFToken: '0xA709eCF2253B18A757214D64F42026Be8F008bD8',
				CFVault: '0xE303a8Cc37C96669C7Ba5aeE1134bb530e766BdF',
				Decimal: 1e18,
				Name: 'ETH去中心化收益基金',
				Introduce:
					'基于Curve的多个ETH池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
			}
		}
	
		HContract = {USDC: {
      CFToken: '0xfF55c4e42D7C2c4f9fd251f62b3469Fb2783954F',
      CFVault: '0xdA5c2472FBcD3ae9F6fAc5694B5e4c2E3c88e4cc',
      USDC: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
      CRV: '0xD533a949740bb3306d119CC777fa900bA034cd52',
      USDCDecimal: 1e6,
      CRVDecimal: 1e18,
      Length: 2,
      Name: '稳定币去中心化收益基金',
      Introduce:
        '基于Curve的多个稳定币池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
    },
    ETH: {
      CFToken: '0xBAe7EC1BAaAe7d5801ad41691A2175Aa11bcba19',
      CFVault: '0xe39fd820B58f83205Db1D9225f28105971c3D309',
      Decimal: 1e18,
      Name: 'ETH去中心化收益基金',
      Introduce:
        '基于Curve的多个ETH池进行投资，每日收到的CRV奖励将转换成相应资产后继续投入。'
    }
    }
		break
}
export {
	Network,
	Contract,
	HContract,
	API_URL,
	OPEN_URL,
	Wallets,
	DappId,
	TTIMER,
	HMarkets,
	LMarkets
}

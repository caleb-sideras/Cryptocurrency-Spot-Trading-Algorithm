<h1 align="center">Hi 👋, I'm Caleb</h1>
<h3 align="center">A Computer Science student who wanted to automate basic spot trading based on certain parameters. This algorithm is designed to prevent losses and take profits. 4 Major exchanges supported. Note: I am not maintaining this project.</h3>

<h3 align="left">Languages:</h3>
<p align="left"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>


<h1>Classes (V2)</h1>

<h3>CurrentPriceStruct</h3>
<p align="left">Stores the current updated price information of a cryptocurrency-pair.</p>

<h3>PriceTickerRest</h3>
<p align="left">Creates non-blocking threads and retreives updated cryptocurrency-pair price information every interval.</p>

<p>Parameters:</p>
<ul>
<li>Stagger: Instance of the Stagger class (described below).</li>
<li>PriceStruct: Instance of the CurrentPriceStruct class (described above).</li>
<li>interval: Interval at which a request would be sent for updated price information.</li>
</ul>


<h3>Stagger</h3>
<p>Involves all the business logic involving the actual buying and selling of a cryptocurrency pair.</p>

<p>Parameters:</p>
<ul>
<li>breakeven: Initial breakeven threshold at which the algorithm starts. If blank, will be set to current cryptocurrency-pair price * (1 + taker fee)</li>
<li>margin: Decimal value that the algorithm will buy/sell at based on the current cryptocurrency-pair price.</li> 
<li>crypto_amount: The amount of crypto you want this algorithm to trade with.</li> 
<li>crypto_pair: The cryptocurrency-pair you want to trade.</li> 
<li>timestr: Current time string.</li> 
<li>Client: The exchange client class initialized with your public and private keys.</li> 
<li>PriceStruct: The CurrentPriceStruct class.</li> 
<li>taker_fee: The fee attributed with your exchange/account.</li>
</ul>


<h3>Example Initlization</h3>
<pre>
from base import FtxClient
import ftxapi
from Stagger import Stagger
from PriceTickerRest import PriceTickerRest
from Stagger import CurrentPriceStruct


Client = FtxClient(api_key=ftxapi.api_key, api_secret=ftxapi.api_secret, subaccount_name=ftxapi.subaccount_name)


taker_fee = Client.get_account_info()['takerFee']
crypto_pair = Client.SYMBOL_LINK
crypto_amount = 3  

instance_currentprice = CurrentPriceStruct()
instance_stagger = Stagger(crypto_pair=crypto_pair, Client=Client,
                           PriceStruct=instance_currentprice, taker_fee=taker_fee, margin=0.005, crypto_amount=crypto_amount)
instance_priceticker = PriceTickerRest(
    instance_stagger, instance_currentprice)
instance_stagger.price_init()
while True:
    instance_stagger.sell_check()
    instance_stagger.buy_check()
</pre>

<h3>Example Outputs</h3>
<p>Started selling 3 LINK at +-0.005 (0.5%) minimum intervals and finished at 3.01 LINK while the price of LINK increased. Note: All trades have to be profitable factoring in the exchange taker fee.<p>
<img src="https://user-images.githubusercontent.com/66019710/156209322-0d277b10-54d7-4f63-a90e-cf55dfa45604.png"/>

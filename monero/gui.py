#!/bin/python
#
# python-monero-cli-gui
# Copyright 2015 rznag
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
# of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import cmd
import monero


menu_a = {1: 'Show balance', 2: 'Create Payment_ID', 3: 'Get recipient for payment id', 4: 'Check for new deposits',
          5: 'Get transaction history', 6: 'Send coins to single address', 7: 'Send coins to multiple addresses'}

menu_b = {'a': 'Create wallet', 'b': 'Configure daemon + wallet'}


def print_menu_a():
    ret = ''
    for i, v in menu_a.iteritems():
        ret += str(i) + ' ' + str(v) + '\n'
    return ret


def print_menu_b():
    ret = ''
    for i, v in menu_b.iteritems():
        ret += str(i) + ' ' + str(v) + '\n'
    return ret


class App(cmd.Cmd):
    monero_api = None

    prompt = '\n\n' + print_menu_a() + '\n' + print_menu_b() + '\nType in a command:'

    def do_a(self, arg):
        print 'Not implemented yet'

    def do_b(self, arg):
        daemon_host = raw_input('Daemon Host [127.0.0.1]:') or '127.0.0.1'
        daemon_port = raw_input('Daemon Port [28081]:') or 28081
        wallet_host = raw_input('Wallet Host [127.0.0.1]:') or '127.0.0.1'
        wallet_port = raw_input('Wallet Port [5001]:') or 5001
        redis_host = 'localhost'
        redis_port = 6379
        site_salt = 'test'
        self.monero_api = monero.Monero(daemon_host, daemon_port, wallet_host, wallet_port, redis_host, redis_port,
                                        site_salt)

    def do_1(self, arg):
        full_balance, unlocked_balance = self.monero_api.GetWalletBalance()
        print float(full_balance / 1000000000000.0)
        print float(unlocked_balance / 1000000000000.0)

    def do_2(self, arg):
        recipient = raw_input('Recipient:')
        deterministic = raw_input('deterministic [true]:') or True
        payment_id = self.monero_api.GetPaymentID(recipient, deterministic)
        print payment_id

    def do_3(self, arg):
        payment_id = raw_input('Payment ID:')
        recipient = self.monero_api.GetRecipient(payment_id)
        print recipient

    def do_4(self, arg):
        payments = self.monero_api.CheckForDeposits()
        print payments

    def do_5(self, arg):
        paymentid = raw_input('CSV List of payment id:') or []
        payments = self.monero_api.GetDepositHistory(paymentid)
        print payments

    def do_6(self, arg):
        address = raw_input('Address:')
        amount = raw_input('Amount:')
        amount_converted = int(float(amount) * 1000000000000)
        paymentid = raw_input('Payment id [None]:') or None
        mixin = raw_input('Mixing [None]:') or None
        tx_hash = self.monero_api.Send(address, amount_converted, paymentid, int(mixin))
        print tx_hash

    def do_7(self, arg):
        address = raw_input('Address:')
        amount = raw_input('Amount:')
        amount_converted = int(float(amount) * 1000000000000)
        paymentid = raw_input('Payment id [None]:') or None
        mixin = raw_input('Mixing [None]:') or None
        tx_hash = self.monero_api.Send(address, amount_converted, paymentid, int(mixin))
        print tx_hash


if __name__ == '__main__':
    App().cmdloop()


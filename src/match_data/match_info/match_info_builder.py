class MatchInfoTableUtil:

    @staticmethod
    def save_match_info(match_info, postgres_connector):
        try:
            match_id = match_info["match_id"]

            try:
                query = "INSERT INTO public.match_info(match_id) VALUES (\'" + match_id + "\')"
                parameters = ()
                postgres_connector.execute_parameterized_insert_query(query, parameters)
            except Exception as e:
                print(str(e))

            partial_query = ""
            parameters = ()
            #build part of query
            for stat in match_info.keys():
                if stat != "match_id":
                    partial_query = partial_query + stat + " = (%s),"
                    parameters = parameters + (match_info[stat],)

            #remove last comma
            partial_query = partial_query[:-1]
            query = "UPDATE public.match_info SET " + partial_query + " WHERE match_id = (%s);"

            parameters = parameters + (match_id,)

            try:
                postgres_connector.execute_parameterized_insert_query(query, parameters)
            except Exception as e:
                print("Error inserting match_info: " + str(e))
        except Exception as e:
            print("Skipping Match info save because of: " + str(e))